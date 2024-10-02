import { FC } from 'react';

interface Props {
  firstname: string;
  lastname: string;
  username: string;
}

const Companion: FC<Props> = ({ username, firstname, lastname }) => {
  return (
    <div className="companion">
      <p>
        {firstname} {lastname}
      </p>
      <p>{username}</p>
    </div>
  );
};

export default Companion;
