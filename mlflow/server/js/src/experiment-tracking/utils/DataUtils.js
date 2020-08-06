import { KIWI_INTERNAL_PREFIX } from '../../common/utils/TagUtils';

export const TEST_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.test';
export const EVAL_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.eval';
export const TRAIN_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.training';

export class DataInfo {
  constructor(content) {
    this.content = content;
  }

  static fromTags = (tags) => {
    const contentTag = Object.values(tags).find((t) => t.getKey() === TRAIN_DATA_TAG);
    if (contentTag === undefined) {
      return undefined;
    }
    return contentTag.getValue();
  };
}
