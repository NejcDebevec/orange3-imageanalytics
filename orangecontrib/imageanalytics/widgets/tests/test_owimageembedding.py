from Orange.data import Table, Domain, StringVariable
from Orange.widgets.tests.base import WidgetTest
from orangecontrib.imageanalytics.widgets.owimageembedding \
    import OWImageEmbedding
from orangecontrib.imageanalytics.widgets.tests.utils import load_images


class DummyCorpus(Table):
    pass


class TestOWImageEmbedding(WidgetTest):
    def setUp(self):
        self.widget = self.create_widget(OWImageEmbedding)

    def test_not_image_data(self):
        """
        It should not fail when there is a data without images.
        GH-45
        GH-46
        """
        table = Table("iris")
        self.send_signal("Images", table)

    def test_none_data(self):
        """
        It should not fail when there is no data.
        GH-46
        """
        table = Table("iris")[:0]
        self.send_signal(self.widget.Inputs.images, table)
        self.send_signal(self.widget.Inputs.images, None)

    def test_data_corpus(self):
        table = load_images()
        table = DummyCorpus(table)

        self.send_signal(self.widget.Inputs.images, table)
        results = self.get_output(self.widget.Outputs.embeddings)

        self.assertEqual(type(results), DummyCorpus)  # check if outputs type
        self.assertEqual(len(results), len(table))

    def test_data_regular_table(self):
        table = load_images()

        self.send_signal(self.widget.Inputs.images, table)
        results = self.get_output(self.widget.Outputs.embeddings)

        self.assertEqual(type(results), Table)  # check if output right type

        # true for zoo since no images are skipped
        self.assertEqual(len(results), len(table))

    def test_skipped_images(self):
        table = load_images()

        self.send_signal(self.widget.Inputs.images, table)
        results = self.get_output(self.widget.Outputs.skipped_images)

        print(table)
        # in case of zoo where all images are present
        self.assertEqual(results, None)

        # all skipped
        del table.domain.metas[0].attributes["origin"]
        table[:, "Images"] = "http://www.none.com/image.jpg"

        self.send_signal(self.widget.Inputs.images, table)
        skipped = self.get_output(self.widget.Outputs.skipped_images)

        self.assertEqual(type(skipped), Table)
        self.assertEqual(len(skipped), len(table))
