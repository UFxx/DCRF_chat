import { FC } from 'react';

interface Props {
  name: string;
}

const User: FC<Props> = ({ name }) => {
  return (
    <div className="user-list__item">
      <p>{name}</p>
    </div>
  );
};

export default User;
