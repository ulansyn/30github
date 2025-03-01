package com.myproject.network;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * ulansyn
 * 2025-03-01 17:47:32
 */
public class EchoServerMultithreaded {
    int port;
    private ExecutorService pool;

    public EchoServerMultithreaded(int port) {
        this.port = port;
        // Используем cached thread pool для динамического создания потоков по мере необходимости
        this.pool = Executors.newCachedThreadPool();
    }

    public void run() {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Multithreaded server started on port " + port);
            System.out.println("Waiting for connections");

            //цикл для подключений
            while (!serverSocket.isClosed()) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected");
                //отправляем обработку клиента в пул потоков
                pool.submit(() -> handleClient(clientSocket));
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            pool.shutdown();
            System.out.println("Multithreaded server stopped");
        }

    }

    private void handleClient(Socket clientSocket) {
        try (
                InputStream input = clientSocket.getInputStream();
                OutputStream output = clientSocket.getOutputStream();
                Scanner scanner = new Scanner(input, "UTF-8");
                PrintWriter writer = new PrintWriter(new OutputStreamWriter(output, "UTF-8"), true);
        ) {
            while (scanner.hasNextLine()) {
                String message = scanner.nextLine();
                System.out.println("Client on " + clientSocket.getInetAddress() + " received : " + message);
                writer.println("EchoServerMultithreaded: " + message);
                if(message.equalsIgnoreCase("bye")) {
                    System.out.println("Client on " + clientSocket.getInetAddress() + " disconnected");
                    break;
                }
            }
        } catch (IOException e) {
            System.out.println("Error while handling client: " + e.getMessage());
            e.printStackTrace();
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                System.out.println("Error while closing client: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
    public static void main(String[] args) {
        int port = 31415;
        EchoServerMultithreaded server = new EchoServerMultithreaded(port);
        server.run();
    }

//    нужно сделать групповой чат
//    нужно написать личные сообщения
//    нужно написать хранение пользователей и тд

}
