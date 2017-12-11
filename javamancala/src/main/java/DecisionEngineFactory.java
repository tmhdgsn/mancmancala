import java.util.HashMap;

public class DecisionEngineFactory {
    Agent agent;
    HashMap<String, DecisionEngine> engines = new HashMap<>();

    public DecisionEngineFactory(Agent agent) {
        this.agent = agent;
        this.engines.put("basic", new BasicDecisionEngine(this.agent));
        this.engines.put("mcts", new MCTSDecisionEngine(this.agent));
    }
}
