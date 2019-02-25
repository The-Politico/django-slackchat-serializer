import React from 'react';
import ellipsize from 'ellipsize';

import getChatType from 'Utils/getChatType';
import getAbsChatPath from 'Utils/getAbsChatPath';
import getSlackURL from 'Utils/getSlackURL';

import BooleanField from './BooleanField';
import PublishDate from './PublishDate';

import styles from './styles.scss';

const ChatItem = (props) => {
  const { id, live, published, publish_time: publishTime } = props;

  const title = props.title ? props.title :
    props.api_id ? `Chat: ${props.api_id}` :
      `Chat: ${id}`;

  return (
    <div className={styles.component + ' chat-item'}>
      <h3><a href={`./${id}/edit`}>{title}</a></h3>
      <p>{ellipsize(props.introduction, 70)}</p>

      <div className='row context'>
        <div className='type col col-sm-6'>
          <p>Type: {getChatType(props.chat_type).name}</p>
        </div>

        <div className='live col col-sm-3'>
          <BooleanField active={live} href={getSlackURL(props)}>Live</BooleanField>
        </div>

        <div className='published col col-sm-3'>
          <BooleanField active={published} href={getAbsChatPath(props)}>Published</BooleanField>
        </div>
      </div>

      <img src={props.meta.image} alt={props.meta.description} />

      <PublishDate>{publishTime}</PublishDate>
    </div>
  );
};

export default ChatItem;
