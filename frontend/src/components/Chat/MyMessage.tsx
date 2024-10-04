import { FC } from 'react';

interface Props {
  message: string;
}

const MyMessage: FC<Props> = ({ message }) => {
  return (
    <div className="my-message">
      <p className="message-username">Вы</p>
      <p>{message}</p>
    </div>
  );
};

export default MyMessage;
