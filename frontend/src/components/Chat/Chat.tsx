import Messages from './Messages';
import MessageInput from './MessageInput';
import Companion from './Companion';
import UserList from './UserList/UserList';
import { useState } from 'react';

function Chat() {
  const [userListOpened, setUserListOpened] = useState(false);
  function toggleUserList() {
    setUserListOpened(!userListOpened);
  }

  return (
    <div
      className={`container ${
        userListOpened
          ? 'container__user-list__opened'
          : 'container__user-list__closed'
      }`}
    >
      <UserList userListOpened={userListOpened} />
      <Companion
        username="alexkhub"
        firstname="Александр"
        lastname="Хубаев"
        toggleUserList={toggleUserList}
        userListOpened={userListOpened}
      />
      <Messages />
      <MessageInput />
    </div>
  );
}

export default Chat;
