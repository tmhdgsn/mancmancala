public class MancalaMessage<String> {
    public String getMsgType() {
        return msgType;
    }

    public String getArgs() {
        return args;
    }

    private final String msgType;
    private final String args;

    public MancalaMessage(String msgType, String args) {
        this.msgType = msgType;
        this.args = args;
    }
}