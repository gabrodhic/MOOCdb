class Upload < ActiveRecord::Base
  attr_accessible :content, :visualization_id, :user_id, :visualization_step_id, :offering_id
  
  has_attached_file :content,
    :url => "/system/:class/:attachment/:visualization_id/:filename", 
    :path => ":rails_root/public:url"
  
  belongs_to :offering

  private

  Paperclip.interpolates :visualization_id  do |attachment, style|
    attachment.instance.visualization_id
  end
end
