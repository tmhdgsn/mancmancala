import jdk.internal.util.xml.impl.Input;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;

import java.io.InputStream;


public class AgentTest {

    private Agent agent;
    private InputStream mockInputStream;
    @Mock
    private DecisionEngine mockEngine;

    @Before
    void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        this.agent = new Agent(mockInputStream, mockEngine, 7, 7);



    }

    @Test
    public void testCanRunAgent() {
        this.agent.play();
        InputStream from_input = new java.io.ByteArrayInputStream("START;SOUTH".getBytes());
        System.setIn(from_input);
        Mockito.when(mockEngine.getMove()).thenReturn(1);
        System.out.println(this.agent.board);
    }

    @After
    public void tearDown() throws Exception {

    }
}