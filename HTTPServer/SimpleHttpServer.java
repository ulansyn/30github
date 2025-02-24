import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;

public class SimpleHttpServer {

    public static void main(String[] args) throws IOException {
        // Создаем HTTP-сервер, который будет слушать на порту 8000
        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);

        // Создаем контекст для обработки GET-запросов по пути "/"
        server.createContext("/", new MyHandler());

        // Создаем контекст для обработки GET-запросов по пути "/hello"
        server.createContext("/hello", new HelloHandler());

        // Запускаем сервер
        server.setExecutor(null); // создает дефолтный executor
        server.start();

        System.out.println("Сервер запущен на порту 8000");
    }

    // Обработчик для корневого пути "/"
    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "Привет, мир!";
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }

    // Обработчик для пути "/hello"
    static class HelloHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "Привет, это ответ на запрос по пути /hello!";
            exchange.sendResponseHeaders(200, response.getBytes().length);
            OutputStream os = exchange.getResponseBody();
            os.write(response.getBytes());
            os.close();
        }
    }
}
