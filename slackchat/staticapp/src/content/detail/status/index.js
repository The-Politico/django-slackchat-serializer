import assign from 'lodash/assign';
import * as infoImport from './infos';
import * as errorImport from './errors';

export const info = assign({}, infoImport);
export const error = assign({}, errorImport);
