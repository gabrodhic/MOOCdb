class UploadsController < ApplicationController
require 'csv'
  before_action :signed_in_user, only: [:index]
  before_action :admin_user, only: [:edit, :create, :destroy, :update] 

  def new
    @upload = Upload.new
    2.times do
      category = @upload.label_categories.build()
      2.times { category.label_tags.build() }
    end
    @user = current_user
  end

  def index
    @ownuploads = current_user.uploads.paginate(page: params[:page])
    @uploads = Upload.where("user_id != ?", current_user.id).paginate(page: params[:page])
  end

  def show
    @upload = Upload.find(params[:id])
  end

  def edit
    @upload = Upload.find(params[:id])
    @user = current_user
  end

  def update
    @upload = Upload.find(params[:id])
    if @upload.update_attributes(update_params)
      flash[:success] = "Project updated"
      redirect_to uploads_path
    else
      render 'edit'
    end
  end
  def create
    #upload file
    @upload = current_user.uploads.build(upload_params)

    #take each row and generate a post associated with it.
    if @upload.save
      posts = []
      CSV.foreach(@upload.csv.path) { |row| posts << row[@upload.column] }
      posts.each do |p|
       @post = @upload.posts.build(content: p)
        @post.save
        @post.to_sentences
      end
      flash[:success] = "Uploaded successfully"
      redirect_to data_upload_path
    else
      render 'new'
    end
  end

  def destroy
    Upload.find(params[:id]).destroy
    flash[:success] = "File deleted."
    redirect_to uploads_path
  end

  private
    def update_params
      params.require(:upload).permit(:instructions,:name, :description, label_categories_attributes: [:id, :upload_id, :content, :_destroy, label_tags_attributes: [:id, :label_category_id, :content, :_destroy]] )
    end

    def upload_params
      params.require(:upload).permit(:csv, :header, :column, :instructions, :sentences, :name, :description, label_categories_attributes: [:id, :upload_id, :content, :_destroy, label_tags_attributes: [:id, :label_category_id, :content, :_destroy]] )
    end

    def admin_user
      redirect_to(root_path) unless current_user.admin?
    end

    def signed_in_user
      redirect_to(root_path) unless current_user != nil
    end  
end
