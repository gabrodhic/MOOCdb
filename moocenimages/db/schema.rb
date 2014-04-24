# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20140403224732) do

  create_table "offerings", force: true do |t|
    t.string   "name"
    t.integer  "visualization_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "platform"
    t.string   "instructor"
    t.date     "start_date"
    t.date     "end_date"
    t.string   "public_data_file_name"
    t.string   "public_data_content_type"
    t.integer  "public_data_file_size"
    t.datetime "public_data_updated_at"
    t.integer  "user_id"
  end

  add_index "offerings", ["user_id"], name: "index_offerings_on_user_id"

  create_table "tags", force: true do |t|
    t.string "name"
  end

  create_table "user_sessions", force: true do |t|
    t.string   "user_session_id", null: false
    t.text     "date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  add_index "user_sessions", ["updated_at"], name: "index_user_sessions_on_updated_at"
  add_index "user_sessions", ["user_session_id"], name: "index_user_sessions_on_user_session_id"

  create_table "users", force: true do |t|
    t.string   "username"
    t.string   "email"
    t.string   "crypted_password"
    t.string   "password_salt"
    t.string   "persistence_token"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "encrypted_password",     default: "",    null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,     null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string   "current_sign_in_ip"
    t.string   "last_sign_in_ip"
    t.boolean  "admin",                  default: false
    t.boolean  "approved",               default: false, null: false
  end

  add_index "users", ["approved"], name: "index_users_on_approved"
  add_index "users", ["email"], name: "index_users_on_email", unique: true
  add_index "users", ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true

  create_table "visualization_steps", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "visualization_types", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "visualizations", force: true do |t|
    t.string   "name"
    t.integer  "visualization_type_id"
    t.integer  "user_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "description"
    t.integer  "tag_id"
    t.string   "thumbnail_file_name"
    t.string   "thumbnail_content_type"
    t.integer  "thumbnail_file_size"
    t.datetime "thumbnail_updated_at"
    t.string   "data_extraction_script_file_name"
    t.string   "data_extraction_script_content_type"
    t.integer  "data_extraction_script_file_size"
    t.datetime "data_extraction_script_updated_at"
    t.string   "data_aggregation_script_file_name"
    t.string   "data_aggregation_script_content_type"
    t.integer  "data_aggregation_script_file_size"
    t.datetime "data_aggregation_script_updated_at"
    t.string   "data_to_visualization_script_file_name"
    t.string   "data_to_visualization_script_content_type"
    t.integer  "data_to_visualization_script_file_size"
    t.datetime "data_to_visualization_script_updated_at"
  end

end
