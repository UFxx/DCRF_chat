import { FC } from 'react';

import MyMessage from './MyMessage';
import Message from './Message';

const Messages: FC = ({}) => {
  return (
    <div className="messages-container">
      <MyMessage message="Сообщение 1" />
      <MyMessage message="Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aliquid id facere laudantium suscipit natus neque temporibus, ab quo non. Voluptate?" />
      <Message message="Сообщение от другого пользователя" />
    </div>
  );
};

export default Messages;
