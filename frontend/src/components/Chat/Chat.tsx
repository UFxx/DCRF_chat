import Messages from './Messages';
import MessageInput from './MessageInput';
import Companion from './Companion';

function Chat() {
  return (
    <div className="container">
      <Companion username="alexkhub" firstname="Александр" lastname="Хубаев" />
      <Messages />
      <MessageInput />
    </div>
  );
}

export default Chat;
