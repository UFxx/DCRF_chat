import { FC } from 'react';
import User from './User';

interface Props {
  userListOpened: boolean;
}

const UserList: FC<Props> = ({ userListOpened }) => {
  return (
    <div className={`user-list__${userListOpened ? 'opened' : 'closed'}`}>
      <User name="Александр Хубаев" />
      <User name="Александр Хубаев" />
      <User name="Александр Хубаев" />
    </div>
  );
};

export default UserList;
