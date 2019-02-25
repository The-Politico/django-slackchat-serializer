import React from 'react';
import format from 'ap-style-date';

const PublishDate = (props) => {
  if (!props.children) { return null; }

  return (
    <p className='publish-time'>
      <em>
        Published {format.longAP(props.children)}
      </em>
    </p>
  );
};

export default PublishDate;
