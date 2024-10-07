import { FC } from 'react';

interface Props {
  username: string;
  name: string;
}

const User: FC<Props> = ({ username, name }) => {
  return (
    <div className="user-list__item">
      <p className="user-list__item-name">{name}</p>
      <p className="user-list__item-username">{username}</p>
    </div>
  );
};

export default User;
