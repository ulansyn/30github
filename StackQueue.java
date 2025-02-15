public class StackQueue {

    public static class Stack<T> {
        private static class Node<T> {
            T value;
            Node<T> next;

            Node(T value) {
                this.value = value;
            }
        }

        private Node<T> top;

        public void push(T value) {
            Node<T> newNode = new Node<>(value);
            newNode.next = top;
            top = newNode;
        }

        public T pop() {
            if (isEmpty()) {
                throw new IllegalStateException("Стек пуст");
            }
            T value = top.value;
            top = top.next;
            return value;
        }

        public T peek() {
            if (isEmpty()) {
                throw new IllegalStateException("Стек пуст");
            }
            return top.value;
        }

        public boolean isEmpty() {
            return top == null;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            Node<T> current = top;
            while (current != null) {
                sb.append(current.value);
                if (current.next != null) {
                    sb.append(" -> ");
                }
                current = current.next;
            }
            return sb.toString();
        }
    }

    public static class Queue<T> {
        private static class Node<T> {
            T value;
            Node<T> next;

            Node(T value) {
                this.value = value;
            }
        }

        private Node<T> head;
        private Node<T> tail;

        public void enqueue(T value) {
            Node<T> newNode = new Node<>(value);
            if (tail != null) {
                tail.next = newNode;
            }
            tail = newNode;
            if (head == null) {
                head = newNode;
            }
        }

        public T dequeue() {
            if (isEmpty()) {
                throw new IllegalStateException("Очередь пуста");
            }
            T value = head.value;
            head = head.next;
            if (head == null) {
                tail = null;
            }
            return value;
        }

        public T peek() {
            if (isEmpty()) {
                throw new IllegalStateException("Очередь пуста");
            }
            return head.value;
        }

        public boolean isEmpty() {
            return head == null;
        }

        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            Node<T> current = head;
            while (current != null) {
                sb.append(current.value);
                if (current.next != null) {
                    sb.append(" <- ");
                }
                current = current.next;
            }
            return sb.toString();
        }
    }

    public static void main(String[] args) {
        System.out.println("Демонстрация стека:");
        Stack<Integer> stack = new Stack<>();
        stack.push(10);
        stack.push(20);
        stack.push(30);
        System.out.println("Стек: " + stack);
        System.out.println("Верхний элемент (peek): " + stack.peek());
        System.out.println("Извлечение элемента (pop): " + stack.pop());
        System.out.println("Стек после pop: " + stack);

        System.out.println("\nДемонстрация очереди:");
        Queue<String> queue = new Queue<>();
        queue.enqueue("A");
        queue.enqueue("B");
        queue.enqueue("C");
        System.out.println("Очередь: " + queue);
        System.out.println("Первый элемент (peek): " + queue.peek());
        System.out.println("Извлечение элемента (dequeue): " + queue.dequeue());
        System.out.println("Очередь после dequeue: " + queue);
    }
}
