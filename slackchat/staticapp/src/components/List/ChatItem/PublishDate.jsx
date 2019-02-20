import React from 'react';
import dateFns from 'date-fns';

const PublishDate = (props) => {
  if (!props.children) { return null; }

  return (
    <p className='publish-time'>
      <em>
        Published {dateFns.format(new Date(props.children), 'MMM. D, YYYY')}
      </em>
    </p>
  );
};

export default PublishDate;
