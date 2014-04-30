class Comment < ActiveRecord::Base
  belongs_to :user, :foreign_key => :user_id
  belongs_to :parent, :foreign_key => :parent_id, :class_name => Comment.name

  # actually only has and belongs to one, but this is necessary to access it
  has_and_belongs_to_many :visualizations

  def visualization
    return visualizations.first
  end
end
