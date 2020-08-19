import {KIWI_INTERNAL_PREFIX} from '../../common/utils/TagUtils';

export const CONTENT_TAG = KIWI_INTERNAL_PREFIX + "training.hyperparameters";

export class HPInfo {

  static fromTags = (tags) => {
    console.log(tags)
    const contentTag = Object.values(tags).find((t) => t.getKey() === CONTENT_TAG);
    if (contentTag === undefined) {
      return undefined;
    }

    return contentTag.getValue();
  };
}
