import { FC } from 'react';
import OpenUserList from './UserList/OpenUserList';

interface Props {
  firstname: string;
  lastname: string;
  username: string;
  userListOpened: boolean;
  toggleUserList: () => void;
}

const Companion: FC<Props> = ({
  username,
  firstname,
  lastname,
  userListOpened,
  toggleUserList
}) => {
  return (
    <div className="companion">
      {
        <OpenUserList
          toggleUserList={toggleUserList}
          userListOpened={userListOpened}
        />
      }
      <p>
        {firstname} {lastname}
      </p>
      <p>{username}</p>
    </div>
  );
};

export default Companion;
