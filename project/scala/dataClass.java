/**
 * Created by mark on 12/5/16.
 */
import edu.illinois.cs.cogcomp.lbjava.classify.Classifier;
import java.util.Arrays;
import java.util.List;

public class dataClass {
    String body, sentiment;
    String[] stopwords = {"a", "able", "about",
            "across", "after", "all", "almost", "also", "am", "among", "an",
            "and", "any", "are", "as", "at", "b", "be", "because", "been",
            "but", "by", "c", "can", "cannot", "could", "d", "dear", "did",
            "do", "does", "e", "either", "else", "ever", "every", "f", "for",
            "from", "g", "get", "got", "h", "had", "has", "have", "he", "her",
            "hers", "him", "his", "how", "however", "i", "if", "in", "into",
            "is", "it", "its", "j", "just", "k", "l", "least", "let", "like",
            "likely", "m", "may", "me", "might", "most", "must", "my",
            "neither", "n", "no", "nor", "not", "o", "of", "off", "often",
            "on", "only", "or", "other", "our", "own", "p", "q", "r", "rather",
            "s", "said", "say", "says", "she", "should", "since", "so", "some",
            "t", "than", "that", "the", "their", "them", "then", "there",
            "these", "they", "this", "tis", "to", "too", "twas", "u", "us",
            "v", "w", "wants", "was", "we", "were", "what", "when", "where",
            "which", "while", "who", "whom", "why", "will", "with", "would",
            "x", "y", "yet", "you", "your", "z"};

    public dataClass(String[] line) {
        sentiment = line[0];
        String dirtytext = line[1].replaceAll("\\W", "");
        for (String word: stopwords){
            dirtytext.replace(word, "");
        }

        body = dirtytext;
    }
    public dataClass(String body) {
        this.body = body.replaceAll("\\W", "");
        sentiment = null;
    }
    public List<String> getWords() {
        return Arrays.asList(body.split("\\s+"));
    }
    public String getsentiment() {
        return sentiment;
    }
}
