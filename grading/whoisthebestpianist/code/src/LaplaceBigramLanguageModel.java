import java.util.*;

/**
 * A Laplace Bigram language model (modified from UnigramLanguageModel.java)
 */
public class LaplaceBigramLanguageModel implements LanguageModel {
    protected Map<String, Integer> unigramCounts;
    protected Map<String, Integer> bigramCounts;
    
    public LaplaceBigramLanguageModel(HolbrookCorpus corpus) {
        unigramCounts = new HashMap<String, Integer>();
        bigramCounts = new HashMap<String, Integer>();
        train(corpus);
    }

    public void train(HolbrookCorpus corpus) {
        for (Sentence sentence : corpus.getData()) {
            for (int i = 0; i < sentence.size(); i++) {
                
                Datum datum = sentence.get(i);
                String word = datum.getWord();
                if (unigramCounts.containsKey(word)) {
                    unigramCounts.put(word, unigramCounts.get(word) + 1);
                } else {
                    unigramCounts.put(word, 1);
                }

                if (i < sentence.size() - 1){
                    String nextword = sentence.get(i+1).getWord();
                    String bigram = word + "," + nextword;
                    if (bigramCounts.containsKey(bigram))
                        bigramCounts.put(bigram, bigramCounts.get(bigram) + 1);
                    else
                        bigramCounts.put(bigram,1);
                }
            }
        }
    }

    public double score(List<String> sentence) {
        double score = 0.0;
        for (int i = 0; i < sentence.size() - 1; i++) {
            String word = sentence.get(i);
            String nextword = sentence.get(i+1);
            String bigram = word + "," + nextword;

            int bigramCount = bigramCounts.containsKey(bigram) ? bigramCounts.get(bigram) : 0;
            int unigramCount = unigramCounts.containsKey(word) ? unigramCounts.get(word) : 0;
            int V = unigramCounts.size();
            
            score += Math.log(bigramCount + 1);
            score -= Math.log(unigramCount + V);
        }
        return score;
    }
}
