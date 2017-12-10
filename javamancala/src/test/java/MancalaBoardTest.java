import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class MancalaBoardTest {

    MancalaBoard mancalaBoard;

    @Before
    public void setUp() throws Exception {
        this.mancalaBoard = new MancalaBoard(7, 7);
    }

    @Test
    public void givenRawStrStateUpdateBoardCorrectly() {
        this.mancalaBoard.updateBoard("0,0,0,0,0,0,0,20,1,21,14,14,13,13,2,1");
        int[][] expected = {
                {0,0,0,0,0,0,0,20},
                {1, 21, 14, 14, 13, 13, 2, 1}
        };
        assertArrayEquals(expected, this.mancalaBoard.board);
    }
}