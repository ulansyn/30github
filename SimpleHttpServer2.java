import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.InetSocketAddress;

public class SimpleHttpServer2 {
    public static void main(String[] args) throws IOException {
        // Создаем сервер на порту 8000
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
        System.out.println("Server started at http://localhost:8000");

        // Контекст для корневого URL "/"
        server.createContext("/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                // Обработка только GET-запросов
                if ("GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                    String response = "Welcome to the simple HTTP server!";
                    exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
                    exchange.sendResponseHeaders(200, response.getBytes("UTF-8").length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes("UTF-8"));
                    os.close();
                } else {
                    // Если метод не GET, возвращаем ошибку 405 Method Not Allowed
                    exchange.sendResponseHeaders(405, -1);
                }
            }
        });

        // Контекст для URL "/echo"
        server.createContext("/echo", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String method = exchange.getRequestMethod();
                if ("GET".equalsIgnoreCase(method)) {
                    String response = "This is the /echo endpoint. Send a POST request with data to echo it back.";
                    exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
                    exchange.sendResponseHeaders(200, response.getBytes("UTF-8").length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes("UTF-8"));
                    os.close();
                } else if ("POST".equalsIgnoreCase(method)) {
                    // Читаем тело запроса
                    InputStream is = exchange.getRequestBody();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
                    StringBuilder requestBody = new StringBuilder();
                    String line;
                    while ((line = reader.readLine()) != null) {
                        requestBody.append(line).append("\n");
                    }
                    reader.close();
                    
                    String response = "Echo:\n" + requestBody.toString();
                    exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
                    exchange.sendResponseHeaders(200, response.getBytes("UTF-8").length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(response.getBytes("UTF-8"));
                    os.close();
                } else {
                    // Если метод не поддерживается, возвращаем 405 Method Not Allowed
                    exchange.sendResponseHeaders(405, -1);
                }
            }
        });

        // Используем стандартный исполнитель для обработки запросов
        server.setExecutor(null);
        server.start();
    }
}
