class Post < ActiveRecord::Base
  has_and_belongs_to_many :users
  belongs_to :upload
  has_many :sentences
  validates :upload_id, presence: true
  validates :content, presence: true

  def to_sentences
    if upload.sentences?
      regex = /[^!\.\r\n\?]*[!|\.|\n|\?][\s]*[\r?\n|]*|[^!\.\r\n\?]*$/
      matches = content.scan(regex)
      n = matches.length - 1
      for index in 0..n
        @sentence = self.sentences.build(content: matches[index])
        @sentence.save
      end
    else
      @sentence = self.sentences.build(content: content)
      @sentence.save
    end
  end

  def highlight_sentence(sentence)
    bolded = self.content.gsub(sentence, "<b>"+sentence+"</b>")
  return bolded
  end

  def label_fields
    labels = {}
    for i in 0..upload.label_categories.length - 1
      label_tags = {}
      for j in 0..upload.label_categories[i].label_tags.length - 1
        label_tags[upload.label_categories[i].label_tags[j].content.to_sym] = upload.label_categories[i].label_tags[j].content
      end
      labels[upload.label_categories[i].content.to_sym] = label_tags
    end
    return labels
  end
end
