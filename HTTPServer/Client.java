import java.io.*; // для BufferedReader, BufferedWriter
import java.net.Socket;

/**
 * ulansyn
 * 2025-02-20 15:48:30
 */
public class Client {
    public static void main(String[] args) {
        try (Socket clientSocket = new Socket("localhost", 4004);
             BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
             BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
             BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()))) {

            System.out.println("Введите сообщение (для выхода наберите 'exit'):");
            String word;
            while ((word = reader.readLine()) != null) {
                // тправляем введённое сообщение на сервер
                out.write(word + "\n");
                out.flush();

                String serverWord = in.readLine();
                if (serverWord == null) break;
                System.out.println("Server: " + serverWord);

                if (word.equalsIgnoreCase("exit")) break;
            }
        } catch (IOException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }
    }
}
