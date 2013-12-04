class VisualizationsController < ApplicationController

  def home

  end

  def index
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
end
