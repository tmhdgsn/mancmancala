import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;

@RunWith(Parameterized.class)
public class BasicDecisionEngineTest {
    private int[] expected_moves = {0, 0, 6, 1};
    private Side[] sides = {Side.SOUTH, Side.NORTH, Side.NORTH, Side.SOUTH};
    Agent agent;

    @Parameters
    public static Collection<Object[]> data() {
        int[][] init_board_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        int[][] init_board_2 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        int[][] init_board_3 = {{0, 0, 0, 0, 0, 0, 8, 19}, {0, 20, 13, 13, 12, 12, 1, 1}};
        int[][] board_state_4 = {{0, 0, 1, 1, 2, 12, 12, 5}, {1, 15, 11, 10, 10, 9, 8, 1}};

        int[][] exp_board_state_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {0, 8, 8, 8, 8, 8, 8, 1}};
        int[][] exp_board_state_2 = {{0, 8, 8, 8, 8, 8, 8, 1}, {7, 7, 7, 7, 7, 7, 7, 0}};
        int[][] exp_board_state_3 = {{0, 0, 0, 0, 0, 0, 0, 20}, {1, 21, 14, 14, 13, 13, 2, 1}};
        int[][] exp_board_state_4 = {{1, 1, 2, 2, 3, 0, 13, 5}, {2, 0, 12, 11, 11, 10, 9, 16}};

        return Arrays.asList(new Object[][] {
                { 0, 0 }, { 1, 1 }, { 2, 1 }, { 3, 2 }, { 4, 3 }, { 5, 5 }, { 6, 8 }
        });
    }

    private int[][] init_board;
    private int[][] expected_board;

    @Before
    public void setUp() throws Exception {
        this.agent = new Agent()
    }

    @Test
    public void testPlayHoleUpdatesMancalaCorrectly(int[][] init, int[][] expected) throws Exception {

    }
}