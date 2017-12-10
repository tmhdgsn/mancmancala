import java.util.Scanner;

public class MancMancalaMCTS {
    public static void main(String[] args) {
        Agent agent = new Agent(
                "basic",
                7, 7,
                new Scanner(System.in)
        );
        agent.play();
    }
}
