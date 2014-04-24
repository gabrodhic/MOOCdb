class Visualization < ActiveRecord::Base
  attr_accessible :name, :visualization_type_id, :user_id, :description, :tag_id, :thumbnail,
                  :data_extraction_script, :data_aggregation_script, :data_to_visualization_script

  has_attached_file :thumbnail

  has_attached_file :data_extraction_script,
                    :url => "/system/:class/:attachment/:id/:filename",
                    :path => ":rails_root/public:url"
  has_attached_file :data_aggregation_script,
                    :url => "/system/:class/:attachment/:id/:filename",
                    :path => ":rails_root/public:url"
  has_attached_file :data_to_visualization_script,
                    :url => "/system/:class/:attachment/:id/:filename",
                    :path => ":rails_root/public:url"

  belongs_to :user
  has_many :offerings
  belongs_to :tag

  private

  Paperclip.interpolates :id  do |attachment, style|
    attachment.instance.id
  end
end
