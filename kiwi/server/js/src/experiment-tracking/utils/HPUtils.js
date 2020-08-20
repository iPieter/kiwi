import {KIWI_INTERNAL_PREFIX} from '../../common/utils/TagUtils';

export const CONTENT_TAG = KIWI_INTERNAL_PREFIX + 'training.hyperparameters';

export class HPInfo {
    static fromTags = (tags) => {
        const contentTag = Object.values(tags).find((t) => t.getKey() === CONTENT_TAG);
        if (contentTag === undefined) {
            return undefined;
        }

        return contentTag.getValue();
    };

    static cdfWithReplacement(i, n, N) {
        return (i / N) ** n;
    }

    static computeVariance(N, cur_data, expected_max_cond_n, pdfs) {
        // this computes the standard error of the max.
        // this is what the std dev of the bootstrap estimates of the mean of the max converges to, as
        // is stated in the last sentence of the summary on page 10 of
        // http://www.stat.cmu.edu/~larry/=stat705/Lecture13.pdf

        let variance_of_max_cond_n = [];
        for (let n in [...Array(N).keys()]) {
            // for a given n, estimate variance with \sum(p(x) * (x-mu)^2), where mu is \sum(p(x) * x).
            let cur_var = 0;
            for (let i in [...Array(N).keys()]) {
                cur_var += (cur_data[i] - expected_max_cond_n[n]) ** 2 * pdfs[n][i];
            }
            cur_var = Math.sqrt(cur_var);
            variance_of_max_cond_n.push(cur_var);
        }
        return variance_of_max_cond_n;
    }

    static samplemax(validationPerformance) {
        validationPerformance.sort();

        const N = validationPerformance.length;

        console.log(N);
        let pdfs = [];
        for (let n = 1; n <= N; n++) {
            // the CDF of the max
            let F_Y_of_y = [];
            for (let i = 1; i <= N; i++) {
                F_Y_of_y.push(this.cdfWithReplacement(i, n, N));
            }

            let f_Y_of_y = [];
            let cur_cdf_val = 0;
            for (let i = 0; i < F_Y_of_y.length; i++) {
                f_Y_of_y.push(F_Y_of_y[i] - cur_cdf_val);

                cur_cdf_val = F_Y_of_y[i];
            }

            pdfs.push(f_Y_of_y);
        }

        console.log(pdfs);

        let expected_max_cond_n = [];
        for (let n = 0; n < N; n++) {
            // for a given n, estimate expected value with \sum(x * p(x)), where p(x) is prob x is max.
            let cur_expected = 0;
            for (let i = 0; i < N; i++) {
                cur_expected = cur_expected + validationPerformance[i] * pdfs[n][i];
            }
            expected_max_cond_n.push(cur_expected);
        }

        let var_of_max_cond_n = this.computeVariance(N, validationPerformance, expected_max_cond_n, pdfs);

        return {
            mean: expected_max_cond_n,
            var: var_of_max_cond_n,
            max: Math.max(...validationPerformance),
            min: Math.min(...validationPerformance),
        };
    }
}
