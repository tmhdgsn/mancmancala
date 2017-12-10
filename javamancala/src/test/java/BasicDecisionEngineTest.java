import org.junit.Before;
import org.junit.Test;

import java.util.Scanner;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

public class BasicDecisionEngineTest {
    private Agent agent;

    @Before
    public void setUp() throws Exception {
        this.agent = new Agent("basic", 7, 7, new Scanner(System.in));
    }

    @Test
    public void testPlayHoleUpdatesMancalaCorrectlyGivenInitGameStartSouthMove0() {
        int[][] init_board_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        int[][] exp_board_state_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {0, 8, 8, 8, 8, 8, 8, 1}};
        this.agent.engine.playHole(0, new MancalaBoard(init_board_1), Side.SOUTH);
        assertEquals(exp_board_state_1, init_board_1);
    }

    @Test
    public void testPlayHoleUpdatesMancalaCorrectlyGivenInitGameStartNorthMove0() {
        int[][] init_board_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        int[][] exp_board_state_2 = {{0, 8, 8, 8, 8, 8, 8, 1}, {7, 7, 7, 7, 7, 7, 7, 0}};
        this.agent.engine.playHole(0, new MancalaBoard(init_board_1), Side.NORTH);
        assertEquals(exp_board_state_2, init_board_1);
    }

    @Test
    public void testPlayHoleUpdatesMancalaCorrectlyGivenRandomGameStartNorthMove6() {
        int[][] init_board_3 = {{0, 0, 0, 0, 0, 0, 8, 19}, {0, 20, 13, 13, 12, 12, 1, 1}};
        MancalaBoard init_board = new MancalaBoard(init_board_3);
        int[][] exp_board_state_3 = {{0, 0, 0, 0, 0, 0, 0, 20}, {1, 21, 14, 14, 13, 13, 2, 1}};
        this.agent.engine.playHole(6, new MancalaBoard(init_board_3), Side.NORTH);
        assertEquals(exp_board_state_3, init_board.board);
    }

    @Test
    public void testPlayHoleUpdatesMancalaCorrectlyGivenRandomGameStartSouthMove1() {
        int[][] init_board_4 = {{0, 0, 1, 1, 2, 12, 12, 5}, {1, 15, 11, 10, 10, 9, 8, 1}};
        MancalaBoard init_board = new MancalaBoard(init_board_4);
        int[][] exp_board_state_4 = {{1, 1, 2, 2, 3, 0, 13, 5}, {2, 0, 12, 11, 11, 10, 9, 16}};
        this.agent.engine.playHole(1, init_board, Side.SOUTH);
        assertEquals(exp_board_state_4, init_board.board);
    }

    @Test
    public void testPlayHoleRepeatsGoIfLastSeedLandsInMancala() {
        int[][] init_board_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        MancalaBoard init_board = new MancalaBoard(init_board_1);
        assertTrue(this.agent.engine.playHole(0, init_board, Side.SOUTH));
    }

    @Test
    public void testPlayHoleDoesNotRepeatGoIfLastSeedDoesNotLandInMancala() {
        int[][] init_board_1 = {{7, 7, 7, 7, 7, 7, 7, 0}, {7, 7, 7, 7, 7, 7, 7, 0}};
        MancalaBoard init_board = new MancalaBoard(init_board_1);
        assertFalse(this.agent.engine.playHole(1, init_board, Side.SOUTH));
    }
}