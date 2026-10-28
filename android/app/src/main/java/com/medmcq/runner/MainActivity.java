package com.medmcq.runner;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/**
 * Bọc mcq_runner (index.html + data/library.js trong assets) vào một WebView.
 * Đề, lịch sử, phiên làm dở nằm trong localStorage của WebView, giữ nguyên khi cập nhật APK
 * (miễn là APK mới ký cùng khóa).
 */
public class MainActivity extends Activity {
    private static final String START_URL = "file:///android_asset/index.html";
    private static final int REQ_OPEN_FILE = 1;
    private static final int REQ_SAVE_FILE = 2;

    private WebView webView;
    private ValueCallback<Uri[]> pendingFileChooser;
    private byte[] pendingSaveBytes;
    private String pendingSaveName;
    private long lastBackPress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        setContentView(webView);

        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);

        webView.addJavascriptInterface(new Bridge(), "AndroidBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri url = request.getUrl();
                if ("file".equals(url.getScheme())) return false;
                // Link ra ngoài (http, mailto…) mở bằng app khác, không thay trang thi.
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, url));
                } catch (ActivityNotFoundException ignored) {
                }
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback,
                                             FileChooserParams params) {
                if (pendingFileChooser != null) pendingFileChooser.onReceiveValue(null);
                pendingFileChooser = callback;
                Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
                pick.addCategory(Intent.CATEGORY_OPENABLE);
                pick.setType("*/*");
                try {
                    startActivityForResult(pick, REQ_OPEN_FILE);
                } catch (ActivityNotFoundException e) {
                    pendingFileChooser = null;
                    return false;
                }
                return true;
            }
        });

        // Bài làm dở được index.html tự lưu vào localStorage và hiện nút "Tiếp tục" khi mở lại.
        webView.loadUrl(START_URL);
    }

    /** Gọi từ downloadBlob() trong index.html. */
    private final class Bridge {
        @JavascriptInterface
        public void saveFile(String filename, String mime, String content) {
            runOnUiThread(() -> {
                pendingSaveBytes = content.getBytes(StandardCharsets.UTF_8);
                pendingSaveName = filename;
                Intent create = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                create.addCategory(Intent.CATEGORY_OPENABLE);
                create.setType(mime == null || mime.isEmpty() ? "application/octet-stream" : mime);
                create.putExtra(Intent.EXTRA_TITLE, filename);
                startActivityForResult(create, REQ_SAVE_FILE);
            });
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_OPEN_FILE) {
            if (pendingFileChooser == null) return;
            Uri uri = (resultCode == RESULT_OK && data != null) ? data.getData() : null;
            pendingFileChooser.onReceiveValue(uri == null ? null : new Uri[]{uri});
            pendingFileChooser = null;
        } else if (requestCode == REQ_SAVE_FILE) {
            byte[] bytes = pendingSaveBytes;
            String name = pendingSaveName;
            pendingSaveBytes = null;
            pendingSaveName = null;
            if (resultCode != RESULT_OK || data == null || data.getData() == null) return;
            if (bytes == null) {
                // Android đã tắt app trong lúc chọn chỗ lưu (máy ít RAM), nội dung xuất bị mất.
                Toast.makeText(this, "Không lưu được, hãy bấm Xuất lại", Toast.LENGTH_LONG).show();
                return;
            }
            try (OutputStream out = getContentResolver().openOutputStream(data.getData(), "wt")) {
                if (out == null) throw new java.io.IOException("Không mở được file");
                out.write(bytes);
                Toast.makeText(this, "Đã lưu " + name, Toast.LENGTH_SHORT).show();
            } catch (Exception e) {
                Toast.makeText(this, "Lưu file thất bại: " + e.getMessage(), Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public void onBackPressed() {
        // Cho index.html xử lý trước: đóng hộp thoại / bảng câu, hoặc từ màn khác quay về Ngân hàng đề.
        webView.evaluateJavascript(
                "(function(){try{return !!(window.app && app.handleBack());}catch(e){return false;}})()",
                handled -> {
                    if (!"true".equals(handled)) exitOnSecondPress();
                });
    }

    private void exitOnSecondPress() {
        long now = System.currentTimeMillis();
        if (now - lastBackPress < 2000) {
            finish();
        } else {
            lastBackPress = now;
            Toast.makeText(this, "Bấm Back lần nữa để thoát", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onDestroy() {
        webView.destroy();
        super.onDestroy();
    }
}
