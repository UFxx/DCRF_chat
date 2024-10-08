import { FC } from 'react';

interface Props {
  userListOpened: boolean;
  toggleUserList: () => void;
}

const OpenUserList: FC<Props> = ({ toggleUserList, userListOpened }) => {
  return (
    <div className="open-user-list__button" onClick={toggleUserList}>
      {userListOpened ? (
        <i className="fas fa-times"></i>
      ) : (
        <i className="fas fa-users"></i>
      )}
    </div>
  );
};

export default OpenUserList;
