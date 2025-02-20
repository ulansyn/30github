import java.io.*; //для BufferedReader, BufferedWriter
import java.net.ServerSocket; //для ServerSocket
import java.net.Socket; //для Socket

/**
 * ulansyn
 * 2025-02-20 15:30:07
 */
public class Server {

    public static void main(String[] args) throws IOException {
        //Серверный сокет

        try (ServerSocket server = new ServerSocket(4004)) {//требуется добавить исключение IOException)
            System.out.println("Server started!");
            //дальше ожидаем подключение от клиента
            //Метод accept() блокирует выполнение до тех пор, пока не подключится клиент. После подключения возвращается объект Socket, представляющий это соединение.
            while (true) {
                try (Socket clientSocket = server.accept();) {
                    System.out.println("Client connected!");
                    BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                    BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
                    //in: Создаётся поток для чтения данных, поступающих от клиента. Поток преобразует байтовый поток в символьный.
                    //out: Создаётся поток для записи данных клиенту. Также происходит преобразование из символьного потока в байты.
                    String message;
                    while ((message = in.readLine()) != null) {
                        System.out.println("Received: " + message);
                        // При получении специального сообщения завершаем цикл
                        if (message.equalsIgnoreCase("exit")) {
                            break;
                        }
                        // Отправляем ответ клиенту
                        out.write(message + "\n");
                        out.flush();
                    }
                    System.out.println("Client disconnected!");
                } catch (IOException e) {
                    System.out.println(e.getMessage());
                }
            }
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }

    }
}
