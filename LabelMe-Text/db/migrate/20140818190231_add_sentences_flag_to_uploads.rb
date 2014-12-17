class AddSentencesFlagToUploads < ActiveRecord::Migration
  def change
    add_column :uploads, :sentences, :boolean
  end
end
