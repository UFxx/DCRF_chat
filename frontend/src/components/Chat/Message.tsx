import { FC } from 'react';

interface Props {
  message: string;
}

const Message: FC<Props> = ({ message }) => {
  return (
    <div className="message">
      <p className="message-username">Не вы</p>
      <p>{message}</p>
    </div>
  );
};

export default Message;
