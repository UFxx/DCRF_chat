import SendMessageIcon from '../../assets/images/send_message.png';

function MessageInput() {
  return (
    <div className="message-input">
      <input type="text" placeholder="Введите сообщение" />
      <img src={SendMessageIcon} alt="" />
    </div>
  );
}

export default MessageInput;
