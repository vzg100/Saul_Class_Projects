import edu.illinois.cs.cogcomp.lbjava.learn._
import edu.illinois.cs.cogcomp.saul.classifier.Learnable

import myDataModel._

object Classifiers {

  object sentimentClassifier extends Learnable[dataClass](twit) {
    def label = Label
    override def feature = using(WordFeatures, BigramFeatures)
    override lazy val classifier = new SparseNetworkLearner()
  }

}