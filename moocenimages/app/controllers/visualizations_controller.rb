class VisualizationsController < ApplicationController
  before_filter :authenticate_user!, :only => [:new]
  
  def index
    tags = Tag.all
    @tags_hash = {}
    tags.each do |tag|
      visualizations = Visualization.where(:tag_id => tag.id)
      @tags_hash[tag.name] = visualizations
    end
  end

  def new
    @visualization = Visualization.new
  end

  def create
    visualization = Visualization.create(params[:visualization])
    visualization.update(:user_id => current_user.id)
    redirect_to '/new_viz_step_2?viz_id=' + visualization.id.to_s
  end
  
  def new_step_2
    @viz_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
  end

  def create_step_2
    viz_id = Integer(params[:viz_id])
    offerings = params[:offering][:name].split(',')
    # TODO: make this work with more than one offering
    offering = Offering.create(params[:offering].merge({:visualization_id => viz_id}))

    tags = Tag.where(:name => params[:tag])

    if tags.length > 0
      tag = tags[0]
    else
      tag = Tag.create(:name => params[:tag])
    end

    Visualization.find(viz_id).update(:tag_id => tag.id)
    redirect_to '/new_viz_step_3?viz_id=' + params[:viz_id] + '&offering_id=' + offering.id.to_s
  end

  def new_step_3
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_3
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_4?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_4
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_4
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_5?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_5
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_5
    @upload = Upload.create(params[:upload])
    redirect_to '/new_viz_step_6?viz_id=' + params[:upload][:visualization_id] + '&offering_id=' + params[:upload][:offering_id]
  end

  def new_step_6
    @viz_id = 0
    @offering_id = 0
    @viz_id = params[:viz_id] if params[:viz_id]
    @offering_id = params[:offering_id] if params[:offering_id]

    @upload = Upload.new
  end

  def create_step_6
    @upload = Upload.create(params[:upload])
    redirect_to '/visualizations/' + params[:upload][:visualization_id]
  end

  def show
    @visualization = Visualization.find(params[:id])
  end

  def get_upload
    begin
      visualization = Visualization.find(params[:visualization_id])
      begin
        offering = visualization.offerings.find(params[:offering_id])
      rescue ActiveRecord::RecordNotFound => e
        render :json => {:contents => "No offerings found for this visualization", :file_name => "File not Found"}
      end
      upload = offering.uploads.find_by_visualization_step_id(params[:visualization_step_id])
      if upload.nil?
        begin
          offering = visualization.offerings.first
        rescue ActiveRecord::RecordNotFound => e
          render :json => {:contents => "No offerings found for this visualization", :file_name => "File not Found"}
        end
        upload = offering.uploads.find_by_visualization_step_id(params[:visualization_step_id])
      end

      upload_contents = File.open(upload.content.path).read
      upload_name = upload.content_file_name

      response = {:contents => upload_contents, :file_name => upload_name}

    rescue ActiveRecord::RecordNotFound => e
      response = {:contents => "This file could not be read.", :file_name => "File Not Found"}
    end
    respond_to do |format|
      format.json {render :json => response}
    end
  end

  def get_zip
    require 'zip'
    require 'uri'

    visualization = Visualization.find(params[:visualization_id])
    offering = visualization.offerings.find(params[:offering_id])
    uploads = offering.uploads

    zipfile_name = '/zips/' + offering.name + '_' + visualization.name + '.zip'
    zipfile_path = 'public' + zipfile_name
    File.delete(zipfile_path) if File.exist?(zipfile_path)

    Zip::File.open(zipfile_path, Zip::File::CREATE) do |zipfile|
      uploads.each do |upload|
        zipfile.add(upload.content_file_name, upload.content.path)
      end
    end
    File.chmod(0644, zipfile_path)

    redirect_to URI.encode(zipfile_name)
  end
end
