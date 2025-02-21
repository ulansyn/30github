import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

public class Main {
    public static void main(String[] args) {
        try {
            HttpServer server = makeServer();
            initRoutes(server);
            server.start();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static HttpServer makeServer() throws IOException {
        String host = "localhost";
        InetSocketAddress address = new InetSocketAddress(host, 8080);

        System.out.printf(
                "Started server on %s:%d",
                address.getHostName(),
                address.getPort()
        );

        HttpServer server = HttpServer.create(address, 50);
        System.out.println("    successfully started");
        return server;
    }

    private static void initRoutes(HttpServer server) {
        server.createContext("/", new FileHandler("src"));
        server.createContext("/apps/", exchange -> handleApps(exchange));
        server.createContext("/apps/profile", exchange -> handleProfile(exchange));
    }

    private static PrintWriter getWriterFrom(HttpExchange exchange) throws IOException {
        OutputStream outputStream = exchange.getResponseBody();
        Charset charset = StandardCharsets.UTF_8;
        return new PrintWriter(outputStream, false, charset);
    }

    private static void write(Writer writer, String msg, String method) {
        String body = String.format("%s: %s%n%n", msg, method);
        try {
            writer.write(body);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void writeHeaders(Writer writer, String type, Headers headers) {
        write(writer, type, "");
        headers.forEach((k, v) -> write(writer, "\t" + k, v.toString()));
    }

    private static BufferedReader getReader(HttpExchange exchange) {
        InputStream inputStream = exchange.getRequestBody();
        Charset charset = StandardCharsets.UTF_8;
        InputStreamReader inputStreamReader = new InputStreamReader(inputStream, charset);
        return new BufferedReader(inputStreamReader);
    }

    private static void writeData(Writer writer, HttpExchange exchange) {
        try (BufferedReader reader = getReader(exchange)) {
            if (!reader.ready()) return;

            write(writer, "Data", "");
            reader.lines().forEach(line -> write(writer, "\t", line));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleRequest(HttpExchange exchange, String responseMessage) {
        try {
            exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
            exchange.sendResponseHeaders(200, 0);

            try (PrintWriter writer = getWriterFrom(exchange)) {
                String method = exchange.getRequestMethod();
                String path = exchange.getHttpContext().getPath();

                write(writer, "HTTP method", method);
                write(writer, "Handler", path);
                writeHeaders(writer, "Request headers", exchange.getRequestHeaders());
                writeData(writer, exchange);

                writer.write("\n" + responseMessage);
                writer.flush();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleRoot(HttpExchange exchange) {
        handleRequest(exchange, "Это корневой путь");
    }

    private static void handleApps(HttpExchange exchange) {
        handleRequest(exchange, "Эта страница для /apps");
    }

    private static void handleProfile(HttpExchange exchange) {
        handleRequest(exchange, "Эта страница для /profile");
    }

}
