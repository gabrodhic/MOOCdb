class Sentence < ActiveRecord::Base
  belongs_to :post
  has_many :responses
  validates :post_id, presence: true
  validates :content, presence: true
end
