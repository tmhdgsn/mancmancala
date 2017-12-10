import org.junit.Test;
import java.util.Scanner;

import static org.junit.Assert.assertTrue;


public class AgentTest {

    @Test
    public void testCanRunAgent() {
        Scanner sc = new Scanner("START;South\nEND");
        Agent agent = new Agent("basic", 7, 7, sc);
        agent.play();
    }

    @Test
    public void testAgentSwapsSides() {
        Scanner sc = new Scanner("START;South\n" +
                "CHANGE;2;8,7,7,7,7,7,7,0,7,0,8,8,8,8,8,1;OPP\n" +
                "CHANGE;SWAP;8,7,7,7,7,7,7,0,7,0,8,8,8,8,8,1;YOU\n" +
                "END");
        Agent agent = new Agent("basic", 7, 7, sc);
        agent.play();
        assertTrue(agent.side == Side.NORTH);
    }
}