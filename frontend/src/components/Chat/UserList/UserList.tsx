import { FC, useCallback, useEffect, useMemo, useState } from 'react';
import User from './User';

interface Props {
  userListOpened: boolean;
}

interface RequestData {
  request_id: number;
  action: string;
  data: object | null;
}

interface Response {
  action: string;
  data: {
    email: string;
    first_name: string;
    id: number;
    last_name: string;
    phone: string;
    username: string;
  }[];
  errors: [];
  request_id: number;
  response_status: number;
}

const UserList: FC<Props> = ({ userListOpened }) => {
  const [users, setUsers] = useState<Response>();
  const socket = new WebSocket('ws://127.0.0.1:8001/ws/new_user/');

  useEffect(() => {
    socket.onopen = () => {
      console.log('Соединение установлено.');

      const data: RequestData = {
        request_id: Date.now(),
        action: 'list',
        data: null
      };
      socket.send(JSON.stringify(data));
    };

    socket.onmessage = (e) => {
      setUsers(JSON.parse(e.data));
    };
  }, []);

  return (
    <div className={`user-list__${userListOpened ? 'opened' : 'closed'}`}>
      {users?.data.map((user) => {
        return (
          <User
            key={user.id}
            username={user.username}
            name={`${user.first_name} ${user.last_name}`}
          />
        );
      })}
    </div>
  );
};

export default UserList;
