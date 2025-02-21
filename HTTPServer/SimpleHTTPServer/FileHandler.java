import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

import java.io.*;
import java.nio.file.Files;

public class FileHandler implements HttpHandler {
    private final String rootDir;

    public FileHandler(String rootDir) {
        this.rootDir = rootDir;
    }


    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
            exchange.sendResponseHeaders(405, -1);
            return;
        }
        String path = exchange.getRequestURI().getPath();
        if (path.equals("/")) {
            path = "/index.html";
        }

        File file = new File(rootDir + path).getCanonicalFile();
        File root = new File(rootDir).getCanonicalFile();

        if (!file.getPath().startsWith(root.getPath())) {
            sendTextResponse(exchange, 404, "Доступа нет");
            return;
        }
        if (!file.exists() || !file.isFile()) {
            sendTextResponse(exchange, 404, "Такого файла нет: " + path);
            return;
        }
        try {
            String contentType = getContentType(file.getName());

            if (contentType == null) {
                sendTextResponse(exchange, 400, "Неподдерживаемый тип файла: " + path);
                return;
            }

            exchange.getResponseHeaders().set("Content-Type", contentType);
            exchange.sendResponseHeaders(200, file.length());
            try (OutputStream os = exchange.getResponseBody()) {
                Files.copy(file.toPath(), os);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            sendTextResponse(exchange, 500, "Ошибка");
        }
    }

    private String getContentType(String name) {
        if (name.endsWith(".html")) {
            return "text/html";
        }
        if (name.endsWith(".css"))
            return "text/css; charset=utf-8";
        if (name.endsWith(".js"))
            return "application/javascript; charset=utf-8";
        if (name.endsWith(".png"))
            return "image/png";
        if (name.endsWith(".jpg") || name.endsWith(".jpeg"))
            return "image/jpeg";
        return null;
    }

    private void sendTextResponse(HttpExchange exchange, int code, String message) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(code, 0);
        try (PrintWriter writer = new PrintWriter(new OutputStreamWriter(exchange.getResponseBody(), "UTF-8"))) {
            writer.write(message);
        }
    }

}
