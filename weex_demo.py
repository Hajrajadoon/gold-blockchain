package com.weex.lcp.utils;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class ApiClient {
    // API Info
    private static final String API_KEY = "weex_e0ee9ae2c9befaee21aa7a03d90f4e48"; // Replace with your actual API Key
    private static final String SECRET_KEY = "15b5a8dd630b866565cf0934c04cc4acbdc77f55c37c69f28306fe2b750b2baa"; // Replace with your actual Secret Key
    private static final String ACCESS_PASSPHRASE = "weex00001214"; // Replace with your actual Access Passphrase
    private static final String BASE_URL = "https://api.weex.com"; // Replace with your actual API address
    // Generate signature (POST request)
    public static String generateSignature(String secretKey, String timestamp, String method, String requestPath, String queryString, String body) throws Exception {
        String message = timestamp + method.toUpperCase() + requestPath + queryString + body;
        return generateHmacSha256Signature(secretKey, message);
    }
    // Generate signature (GET request)
    public static String generateSignatureGet(String secretKey, String timestamp, String method, String requestPath, String queryString) throws Exception {
        String message = timestamp + method.toUpperCase() + requestPath + queryString;
        return generateHmacSha256Signature(secretKey, message);
    }
    // Generate HMAC SHA256 signature
    private static String generateHmacSha256Signature(String secretKey, String message) throws Exception {
        SecretKeySpec secretKeySpec = new SecretKeySpec(secretKey.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(secretKeySpec);
        byte[] signatureBytes = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(signatureBytes);
    }
    // Send POST request
    public static String sendRequestPost(String apiKey, String secretKey, String accessPassphrase, String method, String requestPath, String queryString, String body) throws Exception {
        String timestamp = String.valueOf(System.currentTimeMillis());
        String signature = generateSignature(secretKey, timestamp, method, requestPath, queryString, body);
        HttpPost postRequest = new HttpPost(BASE_URL + requestPath);
        postRequest.setHeader("ACCESS-KEY", apiKey);
        postRequest.setHeader("ACCESS-SIGN", signature);
        postRequest.setHeader("ACCESS-TIMESTAMP", timestamp);
        postRequest.setHeader("ACCESS-PASSPHRASE", accessPassphrase);
        postRequest.setHeader("Content-Type", "application/json");
        postRequest.setHeader("locale", "en-US");
        StringEntity entity = new StringEntity(body, StandardCharsets.UTF_8);
        postRequest.setEntity(entity);
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            CloseableHttpResponse response = httpClient.execute(postRequest);
            return EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
        }
    }
    // Send GET request
    public static String sendRequestGet(String apiKey, String secretKey, String accessPassphrase, String method, String requestPath, String queryString) throws Exception {
        String timestamp = String.valueOf(System.currentTimeMillis());
        String signature = generateSignatureGet(secretKey, timestamp, method, requestPath, queryString);
        HttpGet getRequest = new HttpGet(BASE_URL + requestPath+queryString);
        getRequest.setHeader("ACCESS-KEY", apiKey);
        getRequest.setHeader("ACCESS-SIGN", signature);
        getRequest.setHeader("ACCESS-TIMESTAMP", timestamp);
        getRequest.setHeader("ACCESS-PASSPHRASE", accessPassphrase);
        getRequest.setHeader("Content-Type", "application/json");
        getRequest.setHeader("locale", "en-US");
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            CloseableHttpResponse response = httpClient.execute(getRequest);
            return EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
        }
    }
    // Example usage
    public static void main(String[] args) {
        try {
            // GET request example
            String requestPath = "/api/uni/v3/order/currentPlan";
            String queryString = "?symbol=cmt_bchusdt&delegateType=0&startTime=1742213127794&endTime=1742213506548";
            String response = sendRequestGet(API_KEY, SECRET_KEY, ACCESS_PASSPHRASE, "GET", requestPath, queryString);
            System.out.println("GET Response: " + response);
            // POST request example
             String body = "{\"symbol\": \"ETHUSDT_SPBL\", \"limit\": \"2\"}";
             response = sendRequestPost(API_KEY, SECRET_KEY, ACCESS_PASSPHRASE, "POST", requestPath, "", body);
             System.out.println("POST Response: " + response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
