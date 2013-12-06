class VisualizationsController < ApplicationController

  def home

  end

  def about

  end
  
  def index
    tags = Tag.all
    @tags_hash = {}
    tags.each do |tag|
      visualizations = Visualization.where(:tag_id => tag.id)
      @tags_hash[tag.name] = visualizations
    end

  end

  def new
    @upload = Upload.new
  end
  
  def show
    @visualization = Visualization.find(params[:id])
  end

  def get_upload
    visualization = Visualization.find(params[:visualization_id])
    offering = visualization.offerings.find(params[:offering_id])
    upload = offering.uploads.find_by_visualization_step_id(params[:visualization_step_id])

    upload_contents = File.open(upload.content.path).read
    upload_name = upload.content_file_name

    respond_to do |format|
      format.json {render :json => {:contents => upload_contents, :file_name => upload_name}}
    end
  end

  def get_zip
    require 'zip'
    require 'uri'

    visualization = Visualization.find(params[:visualization_id])
    offering = visualization.offerings.find(params[:offering_id])
    uploads = offering.uploads

    zipfile_name = '/' + offering.name + '_' + visualization.name + '.zip'
    zipfile_path = 'public' + zipfile_name
    File.delete(zipfile_path) if File.exist?(zipfile_path)

    Zip::File.open(zipfile_path, Zip::File::CREATE) do |zipfile|
      uploads.each do |upload|
        zipfile.add(upload.content_file_name, upload.content.path)
      end
    end

    redirect_to URI.encode(zipfile_name)
  end
end
