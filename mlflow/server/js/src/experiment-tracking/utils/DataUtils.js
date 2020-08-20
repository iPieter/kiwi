import { KIWI_INTERNAL_PREFIX } from '../../common/utils/TagUtils';

export const TRAIN_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.training';
export const TRAINDEV_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.traindev';
export const DEV_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.dev';
export const TEST_DATA_TAG = KIWI_INTERNAL_PREFIX + 'datasets.test';

export class DataInfo {
  constructor(content) {
    this.content = content;
  }

  static getTag = (tags, tagType) => {
    const tag = {};

    Object.values(tags)
      .filter((t) => t.getKey().includes(tagType))
      .forEach((t) => (tag[t['key'].split('.')[3]] = t['value']));
    if (tag === undefined) {
      return [];
    }
    return tag;
  };

  static fromTags = (tags) => {
    return {
      train: this.getTag(tags, TRAIN_DATA_TAG),
      traindev: this.getTag(tags, TRAINDEV_DATA_TAG),
      dev: this.getTag(tags, DEV_DATA_TAG),
      test: this.getTag(tags, TEST_DATA_TAG),
    };
  };
}
