
import edu.illinois.cs.cogcomp.saul.datamodel.DataModel

import scala.collection.JavaConversions._

object myDataModel extends DataModel {

  val twit = node[dataClass]

  val WordFeatures = property(twit) {
    x: dataClass =>
      val a = x.getWords.toList
      a
  }

  val BigramFeatures = property(twit) {
    x: dataClass => x.getWords.toList.sliding(2).map(_.mkString("-")).toList
  }

  val Label = property(twit) {
    x: dataClass => x.getsentiment
  }}